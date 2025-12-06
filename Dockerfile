FROM python:3.9-slim

WORKDIR /radar

# מעתיקים את כל קבצי האפליקציה
COPY radar_sim/ /radar/

# מתקינים Flask ישירות
RUN pip install --no-cache-dir flask

EXPOSE 5000

CMD ["python", "app.py"]
