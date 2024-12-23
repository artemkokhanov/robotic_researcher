"""
The main module that calls a robot to fetch information about a list of
scientists.
"""
from config_loader import ConfigLoader
from robotics import Robot

# Load config
config_loader = ConfigLoader('config.yaml')
config = config_loader.get_config()

# Initialize robot
robot = Robot("Roboto", config)


def main() -> None:
    """
    The main function of the program.
    Controls the robot's actions.
    The robot first says hello, then it fetches the information about
    the given scientists, then it finally says goodbye and gracefully closes
    the browsers.
    """
    try:
        robot.say_hello()
        robot.open_browser()
        robot.get_scientists_information()
        robot.say_goodbye()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        robot.close_all_browsers()


if __name__ == "__main__":
    main()
