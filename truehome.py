import devices
import groups
import rooms


if __name__ == '__main__':
    # Add devices to observer
    for device in groups.all:
        devices.observer.add_device(device)

    # Create logic for each room
    bedroom = rooms.Bedroom()
    living_room = rooms.LivingRoom()

    # Run observer
    devices.observer.run()
