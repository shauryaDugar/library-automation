import cv2
from pyzbar import pyzbar
import requests
import datetime
import argparse
from utils import get_info

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="libraryAuto/Logs/barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())


# Initialize the camera
print("[INFO] starting video stream...")
camera = cv2.VideoCapture(0)

csv = open(args["output"], "w")

# Set the resolution of the camera
camera.set(3, 640)
camera.set(4, 480)

# Initialize a list to keep track of the people who have entered the room and their entry times
people_in_room = []

while True:
    # Capture a frame from the camera. Here ret returns True or False depending on whether 
    # the frame is available or not. frame is the frame itself.
    ret, frame = camera.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes in the frame
    codes = pyzbar.decode(gray)

    # Loop over all detected codes
    for code in codes:
        # Extract the QR code's data
        data = code.data.decode("utf-8")

        # Draw a box around the detected QR code
        (x, y, w, h) = code.rect

        # Draw the decoded information on the screen
        if get_info(data) is not None:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            error="Invalid Barcode!"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, error, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            break

        # If the person has not already entered the room, add them to the list and send an HTTP request to update the count
        if data not in people_in_room:
            people_in_room.append(data)
            time = datetime.datetime.now()
            num_people = len(people_in_room)
            url = f"http://localhost:8000/update_count?count={num_people}"
            requests.get(url)
            #Send an email to user once entry into the library is detected
            mail_url = f"http://localhost:8000/send_mail?reg_no={data}&time={time}"
            r = requests.get(mail_url)
            # Print a confirmation message
            print(f"Person {data} entered the room at {time}. {num_people} people in the room.")
            
            csv.write("{},{}\n".format(time, data))
            csv.flush()

    # Display the frame on the screen
    cv2.imshow("QR Code Scanner", frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources
camera.release()
cv2.destroyAllWindows()
