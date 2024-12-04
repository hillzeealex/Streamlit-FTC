# Streamlit-FTC-
Streamlit for fit-tes-courses

 # create an image from an environment
FROM python:3.10.6
WORKDIR /fit_tes_courses

# RUN run terminal command
COPY fit_tes_courses fit_tes_courses
COPY requirements_prod.txt requirements_prod.txt

RUN pip install --no-cache-dir -r requirements_prod.txt

# install your package
COPY fit_tes_courses/model model
COPY setup.py setup.py

RUN pip install .

EXPOSE 8000
# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uvicorn", "fit_tes_courses.app.api:app", "--host", "0.0.0.0", "--port", "8080"]
