from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import generics, permissions
from .models import ContactMessage
from .serializers import ContactMessageSerializer


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer



class ContactMessageCreateView_0(generics.CreateAPIView):
    """
    API endpoint for visitors to submit contact form messages.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]  #
    
    
    def perform_create(self, serializer):
        # Save to database
        contact = serializer.save()

        # Prepare email
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails="sbas.aog@gmail.com",  # replace with your recruiter/admin email
            subject=f"New Contact Message from {contact.name}",
            html_content=f"""
                <p><strong>Name:</strong> {contact.name}</p>
                <p><strong>Email:</strong> {contact.email}</p>
                <p><strong>Message:</strong></p>
                <p>{contact.message}</p>
            """
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            print(f"Error sending email: {e}")





class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        # Prepare notification email (to admin)
        admin_email = settings.DEFAULT_FROM_EMAIL
        subject_admin = f"New Contact Message from {message.name}"
        content_admin = f"""
        You have received a new message:

        Name: {message.name}
        Email: {message.email}
        Message:
        {message.message}
        """
        admin_mail = Mail(
            from_email=admin_email,
            to_emails=admin_email,
            subject=subject_admin,
            plain_text_content=content_admin
        )

        # Prepare feedback email (to sender)
        subject_user = "Thank you for contacting ayigotech"
        content_user = f"""
        Hi {message.name},

        Thank you for reaching out to ayigotech. Your message is well received:

        "{message.message}"
        
        Kindly expect response ASAP

        Best regards,  
        ayigotech.
        """
        user_mail = Mail(
            from_email=admin_email,
            to_emails=message.email,
            subject=subject_user,
            plain_text_content=content_user
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(admin_mail)  # send to admin
            sg.send(user_mail)   # send feedback to sender
        except Exception as e:
            print(f"SendGrid error: {e}")

        return Response(
            {"detail": "Message sent successfully, and confirmation email delivered."},
            status=status.HTTP_201_CREATED
        )