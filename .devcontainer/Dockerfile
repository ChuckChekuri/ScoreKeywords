FROM python:3.13-slim


# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   gcc \
	   postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
USER appuser
    
WORKDIR /home/appuser/scorekeywords
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
