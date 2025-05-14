import cv2
import numpy as np

def show(title, image, centers=[],grid=True):
    while True:
        if grid:
            x=0
            while x<265:
                cv2.rectangle(image, (x, 0),(x+65, 390), (255, 255, 255), 1)
                x+=65
            
            y=0
            while y<361:
                cv2.rectangle(image, (0, y),(264, y+36), (255, 255, 255), 1)
                y+=36
            
        for c1,c2 in centers:
            cv2.circle(image, (c1,c2), 10, (255,255,255))        
        cv2.imshow(title,image)
        if cv2.waitKey(20) &0xFF == ord('d'):
            break
    cv2.destroyAllWindows()

threshold_value=100
def manual_threshold(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = np.zeros_like(gray_image)
    
    rows, cols = gray_image.shape
    for i in range(rows):
        for j in range(cols):
            binary_image[i, j] = 255 if gray_image[i, j] < threshold_value else 0
    
    return binary_image

#This function returns a list of bobbles where each bubblr is a list of (x,y) coordinates that make uo the bubbel
def find_bubbles(img):
    rows, cols = img.shape
    visited = np.zeros_like(img, dtype=bool)
    bubbles = []

    def flood_fill(x, y):
        stack = [(x, y)]
        region = []

        while stack:
            cx, cy = stack.pop()
            if cx < 0 or cy < 0 or cx >= rows or cy >= cols:
                continue
            if visited[cx, cy] or img[cx, cy] == 0:
                continue

            visited[cx, cy] = True
            region.append((cx, cy))
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

        return region

    for i in range(rows):
        for j in range(cols):
            if img[i, j] == 255 and not visited[i, j]:
                region = flood_fill(i, j)
                if len(region) > 50:
                    bubbles.append(region)

    return bubbles

#This function will return a list of coordinates that represent the center points of bubbles
def find_center_of_bubbles(bubbles):
    centers = []
    for bubble in bubbles:
        x_coords = [p[1] for p in bubble]
        y_coords = [p[0] for p in bubble]
        center_x = sum(x_coords) // len(x_coords)
        center_y = sum(y_coords) // len(y_coords)
        centers.append((center_x, center_y))
    return centers

def mark(centers,answer_key):
    answer_sheet=[
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        ]
    
    missing=0
    multiple=0
    between=0
    correct=0
    wrong=0
    
    answer=["","","","","","","","","",""]
    
    
    for c in centers:
        question=int(c[1]/36)
        option=int(c[0]/65)
        marked=False
        
        if ( c[1]%36 >29 or c[1]%36 < 7 ) and not(marked):
            question=-1
            between+=1
            marked=True
        
        if ( c[0]%65 >59 or c[0]%65 < 7 ) and not(marked):
            option=-1
            between+=1
            marked=True
            
        if question>=0 and option>=0:
            answer_sheet[question][option]=1
            marked=True

    #Check for multiple options selected or no options selected
    for x in range(0,10):
        if answer_sheet[x].count(1) > 1:
            answer_sheet[x]=[0,0,0,0]
            multiple+=1
            answer[x]="multiple"
        elif answer_sheet[x].count(1) < 1:
            answer_sheet[x]=[0,0,0,0]
            missing+=1
            answer[x]="missing"
        else:
            if answer_sheet[x][0] == 1:
                answer[x]='a'
            elif answer_sheet[x][1] == 1:
                answer[x]='b'
            elif answer_sheet[x][2] == 1:
                answer[x]='c'
            else:
                answer[x]='d'
                
            if answer_key[x+1] == answer[x]:
                answer[x]="CORRECT"
                correct+=1
            else:
                answer[x]="WRONG"
                wrong+=1
    
    print("Total Question   = 10")
    print("Not Attempted    = " + str(missing ))
    print("Wrongly Marked   = " + str(between ))
    print("Multiple Marked  = " + str(multiple ))
    print("Wrong            = " + str(wrong ))
    print("Correct          = " + str(correct ))
    
    marks= correct - multiple - between
    return marks
    
    
def main(image_path):
    
    answer_key = {
        1: 'c', 
        2: 'b',
        3: 'a',
        4: 'd',
        5: 'a',
        6: 'c',
        7: 'b',
        8: 'b',
        9: 'a',
        10: 'd'
        }
    
    
    image = cv2.imread(image_path)
    
    show("Orignal",image,grid=False)
    
    image= cv2.resize(image, (300,400))
    image=image[40:,40:]
    
    show("After Pre Processing",image,grid=False)
    
    image = manual_threshold(image)
    
    show("After Threshlding",image,grid=False)

    bubbles = find_bubbles(image)

    centers = find_center_of_bubbles(bubbles)
    
    show("With Centers",image,centers,grid=False)
    
    
    marks=0
    marks = mark(centers,answer_key)
    
        
    print("\nTotal Marks      = 10" )
    print("Marks Obtained   = " + str(marks ))


# Path to your bubble sheet image
image_path = "between.jpg"
main(image_path)
