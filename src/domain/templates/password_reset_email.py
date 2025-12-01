def get_password_reset_email_template(reset_token: str) -> tuple[str, str]:
    subject = "Password Reset Request"
    
    body = f""" You requested a password reset. Click the link below:

http://localhost:8000/auth/reset-validate-token?token={reset_token}

This link expires in 1 hour.

If you didn't request this, ignore this email.
"""
    
    return subject, body
