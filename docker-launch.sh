#!/bin/bash

# Whenever command is used incorrectly, print usage
print_usage() {
    echo "Usage: ./docker-launch.sh [build|start|init|restart|execute|stop|clean]"
    exit 1
}

# Ensure program is used correctly
if [[ $# < 1 ]] ; then
    print_usage
fi

# Build container
build_container() {
    docker-compose build
}

# Start container
start_container() {
    docker-compose up
}

# Initalize the application
init_container() {
    docker-compose exec web ./manage.py migrate
    docker-compose exec web ./manage.py loaddata app/fixtures/initial_data.json
    docker-compose exec web ./manage.py createsuperuser
}

# Stop and remove containers 
stop_container() {
    docker-compose stop
}

# Run command in container
execute_container() {
    docker-compose exec web $@
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
       start_container
    ;;
    "stop")
       stop_container
    ;;
    "execute")
       execute_container "${*:2}"
    ;;
    "clean")
        # Prune cache 
        docker-compose stop
        rm db.sqlite3
    ;;
    *)
        print_usage
    ;;
esac
