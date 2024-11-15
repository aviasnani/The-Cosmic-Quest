import os

class Config:
  DEBUG=True
  SECRET_KEY='timelineismalleable'
  SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'database.db')}"
  MONGO_URI = "mongodb://localhost:27017/chapter_quizzes"
  NASA_API_KEY = "oKVg0TFJ118VhEtWSIzkBrj1xDqAQSCXcJTD0v3S"
  SQLALCHEMY_TRACK_MODIFICATIONS = False

