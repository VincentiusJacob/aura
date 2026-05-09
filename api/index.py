from backend.app import app

# Vercel needs the app variable to be exposed
if __name__ == "__main__":
    app.run()
