from rotary_ai import app

# Expose the WSGI callable as "application"
application = app

if __name__ == "__main__":
    # Run the Flask development server (not used in production)
    app.run(host="0.0.0.0", port=8000, debug=True)
