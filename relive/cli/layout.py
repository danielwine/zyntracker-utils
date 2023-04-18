
def get_layout(mx, my):
    return {
        'standard': {
            'header': [2, mx, 0, 0, 0],
            'footer': [1, mx, my, 0, 3],
            'console': [1, int(mx / 2) - 1, my - 3, 0, 1]
        },
        'message': {
            'messages': [
                int(my / 2.5), int(mx / 2) - 1, int(my / 2), 0, 1]
        },
        'data': {
            'status': [1, int(mx/1.6), 1, 0, 1],
            'status2': [1, int(mx/2), 1, int(mx/1.6), 1],
            'sequences': [int(my / 2.5), int(mx / 4), 3, 0, 1],
            'window2': [int(my / 2.5), int(mx / 4), 3, int(mx/4), 1]
        },
        'pattern': {
            'pattern': [my-3, int(mx / 2), 3, int(mx/2), 4]
        }
    }
