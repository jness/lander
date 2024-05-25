#!/bin/bash

# Whenever command is used incorrectly, print usage
print_usage() {
    echo "Usage: ./podman-launch.sh [build|start|init|restart|stop|clean]"
    exit 1
}

# Ensure program is used correctly
if [[ $# < 1 ]] ; then
    print_usage
fi

# Build container
build_container() {
    sudo podman build -t lander .
}

# Start container
start_container() {
    sudo podman run --replace -d -p 8000:8000 \
        --name lander \
        --env-file .env -v .:/app -w /app \
        lander bash -c "cron && python3 manage.py runserver 0.0.0.0:8000"
}

# Initalize the application
init_container() {
    sudo podman exec lander python3 manage.py migrate
    sudo podman exec lander python3 manage.py loaddata app/fixtures/initial_data.json
    sudo podman exec -it lander python3 manage.py createsuperuser
    sudo podman exec -it lander python3 manage.py create_totp 1
}

# Stop and remove containers 
stop_container() {
   sudo podman stop lander
   sudo podman rm lander
}

# Command verb switch
case $1 in
    "build")
        build_container
    ;;
    "start")
        start_container
    ;;
    "init")
       init_container 
    ;;
    "restart")
        # Stop, remove, and then build and start containers
       stop_container
       build_container
       start_container
    ;;
    "stop")
       stop_container
    ;;
    "clean")
        # Prune cache 
        sudo podman system prune
        rm db.sqlite3
    ;;
    *)
        print_usage
    ;;
esac
