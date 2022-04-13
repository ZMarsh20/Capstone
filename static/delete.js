function deleter(i) {
    if (confirm("Are you sure you want to remove this event?\nIf it is past the event's start time it will remain in the database but will not be accessible")){
        location.assign("\\delete\\" + i);
    }
    else {
        location.assign("\\");
    }
}