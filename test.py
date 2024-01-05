def loadFile(input_file):
        with open(input_file, 'r') as file:
            lines = file.read().splitlines()

        # Extract map size and map data
        map_size = int(lines[0])
        map_data = lines[1:]

        # Initialize the map with empty rooms
        game_map = [['-' for _ in range(map_size)] for _ in range(map_size)]

        # Update the map based on input data
        for i in range(map_size):
            room_info = map_data[i].split('.')
            for j, info in enumerate(room_info):
                if info != '-':
                    game_map[i][j] = info

loadFile('map1.txt')