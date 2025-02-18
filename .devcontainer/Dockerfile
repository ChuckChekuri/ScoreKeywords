FROM python:3.13-slim

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   gcc \
	   postgresql-client \
	   git \
	   curl \
	   sudo \
	&& rm -rf /var/lib/apt/lists/*

# Create appuser and add to sudo group
RUN useradd -m appuser \
    && echo "appuser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/appuser \
    && chmod 0440 /etc/sudoers.d/appuser \
	&& mkdir -p /home/appuser/.vscode-server/bin \
    && mkdir -p /home/appuser/.vscode-server/extensions \
    && chown -R appuser:appuser /home/appuser/.vscode-server

# Create and configure virtualenv
ENV VIRTUAL_ENV=/home/appuser/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Change ownership
RUN chown -R appuser:appuser $VIRTUAL_ENV

USER appuser
# Verify sudo access in postCreateCommand
RUN sudo echo "Sudo access confirmed"
    
WORKDIR /home/appuser/scorekeywords

# Now pip install will use the virtualenv
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
