def calculate_box_coordinates(position, length):
    x, y, z = position
    length_x, length_y, length_z = length

    # Calculate the coordinates of the box's corners
    corners = [
        (x, y, z),
        (x + length_x, y, z),
        (x, y + length_y, z),
        (x, y, z + length_z),
        (x + length_x, y + length_y, z),
        (x + length_x, y, z + length_z),
        (x, y + length_y, z + length_z),
        (x + length_x, y + length_y, z + length_z)
    ]

    return corners

# Input the position and length coordinates
x = float(input("Enter the X-coordinate of the position: "))
y = float(input("Enter the Y-coordinate of the position: "))
z = float(input("Enter the Z-coordinate of the position: "))

length_x = float(input("Enter the length in the X-direction: "))
length_y = float(input("Enter the length in the Y-direction: "))
length_z = float(input("Enter the length in the Z-direction: "))

position = (x, y, z)
length = (length_x, length_y, length_z)

# Calculate and print the coordinates of the box's corners
box_coordinates = calculate_box_coordinates(position, length)
for i, corner in enumerate(box_coordinates):
    print(f"Corner {i+1}: {corner}")
