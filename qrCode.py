import cv2
from pyzbar import pyzbar
import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

# Initialize the camera
camera = cv2.VideoCapture(0)

# Set the resolution of the camera
camera.set(3, 640)
camera.set(4, 480)

while True:
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes in the frame
    codes = pyzbar.decode(gray)

    # Loop over all detected codes
    for code in codes:
        # Extract the QR code's data
        data = code.data.decode("utf-8")

        # Update the database with the QR code data
        c.execute("UPDATE mytable SET status = 'Scanned' WHERE code = ?", (data,))
        conn.commit()

        # Print a confirmation message
        print(f"Updated status for QR code {data}")

    # Display the frame on the screen
    cv2.imshow("QR Code Scanner", frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources
camera.release()
cv2.destroyAllWindows()

# Close the database connection
conn.close()
