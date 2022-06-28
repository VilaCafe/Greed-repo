class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
            _points (int) = The points total for the game.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._points = 500
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        player = cast.get_first_actor("player")
        velocity = self._keyboard_service.get_direction()
        player.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("points")
        player = cast.get_first_actor("player")
        gems = cast.get_actors("gems")
        stones = cast.get_actors("stones")
        points = self._points
        

        banner.set_text("Points %s" % (points))
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        player.move_next(max_x, max_y)
        #If the points hit 0, then the 'game over' screen is displayed.
        if points <= 0:
            self._video_service._game_over()
            self._points = 500
        #Adds points to the player's total if they make contact with a gem.
        for gem in gems:
            gem.fall(max_y)
            if player.get_position().equals(gem.get_position()):
                self._points += 10
                gem.change_x()
            if gem.get_position().get_y() == 0:
                gem.change_x()
        #Subtracts points from the player's total if the player makes contact with a stone.
        for stone in stones:
            stone.fall(max_y)
            if player.get_position().equals(stone.get_position()):
                self._points -= 50
                stone.change_x()
            if stone.get_position().get_y() == 0:
                stone.change_x()

        

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()
