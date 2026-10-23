import models
from database import engine

models.Base.metadata.create_all(bind=engine)

# First time print
print("Everything is working son. Go check pgAdmin")