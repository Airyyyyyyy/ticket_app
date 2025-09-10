from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail
from .models import Ticket

def agent_login(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_ticket')
            else:
                error = "Invalid username or password."
        else:
            # Extract error messages from form
            for field, errors in form.errors.items():
                error = errors[0]
                break
    else:
            form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form, 'error': error})

def agent_signup(request):
    error = None
    if request.method == 'POST':
        agent_code = request.POST.get('agent_code')
        password = request.POST.get('password')

        if User.objects.filter(username=agent_code).exists():
            error = "Agent Code already exists."
        else:
            user = User.objects.create(
                username=agent_code,
                password=make_password(password)
            )
            # Automatically log the user in after signup
            login(request, user)
            return redirect('create_ticket')
    return render(request, 'signup.html', {'error': error})

def agent_logout(request):
    logout(request)
    return redirect('agent_login')

@login_required
def create_ticket(request):
    if request.method == 'POST':
        agent_id = request.user.username
        description = request.POST.get('description')
        status = request.POST.get('status')
        category = request.POST.get('category')
        location = request.POST.get('location')

        # Create the ticket manually
        ticket = Ticket.objects.create(
            agent_id=agent_id,
            description=description,
            status=status,
            category=category,
            location=location,
        )

        send_mail(
            subject=f"New Ticket Submitted: {ticket.ticket_id}",
            message=f"Hi Support Team,\n A new ticket has been created and requires your attention.\n\nAgent ID: {agent_id}",    
            from_email=settings.DEFAULT_FROM_EMAIL,       
            recipient_list=['Abdulmaleeq.l@kadickintegrated.com'],
            fail_silently=False,
            html_message=f"""
                <div style="font-family:comic-sans; font-size:20px; padding:24px;">
                    <h2 style="color:black; margin-bottom:16px; text-align:center;">New Ticket.</h2>
                    <p style="color:black; font-weight:300; margin-bottom:40px;">
                        Hi Support Team,<br>
                        A new ticket has been created and requires your attention.<br><br><br>
                        <strong>Agent ID:</strong> {agent_id}<br>
                        <strong>Description:</strong> {description}<br>
                    </p>
                    <div style="color:black; font-weight:300; margin-bottom:40px;">
                        Please login to the ticket portal and treat this ticket.<br><br>
                        Best Regards,<br>
                        Kadick Automated Ticketing System
                    </div>
                </div>
            """
        )
        return redirect('ticket_success', ticket_id=ticket.id)

    return render(request, 'create_ticket.html')

@login_required
def ticket_success(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'ticket_success.html', {'ticket' : ticket})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(agent_id=request.user.username).order_by('-created_at')
    return render(request, 'ticket_list.html', {'tickets': tickets})