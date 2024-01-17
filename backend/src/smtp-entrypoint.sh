echo "Starting SMTP server"
python -m smtpd -c DebuggingServer -n 0.0.0.0:1025
