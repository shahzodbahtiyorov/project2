#!/bin/bash

echo "[RUN SCRIPT] Setting up trap ..."

prep_term() {
    unset term_child_pid
    unset term_kill_needed
    trap 'handle_term' TERM INT
}

handle_term() {
    if [ "${term_child_pid}" ]; then
        kill -TERM "${term_child_pid}" 2>/dev/null
    else
        term_kill_needed="yes"
    fi
}

wait_term() {
    term_child_pid=$!
    if [ "${term_kill_needed}" ]; then
      kill -TERM "${term_child_pid}" 2>/dev/null
    fi
    wait ${term_child_pid} 2>/dev/null
    trap - TERM INT
    wait ${term_child_pid} 2>/dev/null
}

# Prepare termination signal
prep_term

echo "[RUN SCRIPT] Trap setup completed ..."

# Include all your commands to this block
###############################################################
echo "[RUN SCRIPT] Starting app ...";

echo "[RUN SCRIPT] APPLICATION is $APPLICATION"

# Select application to run
case $APPLICATION in
    # Django backend
    django)

        # Collect and upload static files to s3
        python manage.py collectstatic --noinput

        # Run DB migrations
        python manage.py migrate

        ## Custom command
        python manage.py installapp

        # Run server
        # python manage.py runserver 0.0.0.0:8000 &
        gunicorn api.wsgi:application --bind 0.0.0.0:8000 -w 4 -k gevent &

        wait_term
        echo "[RUN SCRIPT] Received stop signal, stopping app ..."
        ;;

    celery_worker)

        # Run application
        celery -A api worker --loglevel=info --concurrency=1 &

        wait_term
        echo "[RUN SCRIPT] Received stop signal, stopping app ..."
        ;;

    celery_beat)

        # Run application
        celery -A api beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

        wait_term
        echo "[RUN SCRIPT] Received stop signal, stopping app ..."
        ;;

    *)
        echo "[RUN SCRIPT] No application specified"
        ;;
esac
###############################################################

# Do some cleanup if needed

echo "[RUN SCRIPT] Stopped, exiting from script ...";
