import os
import numpy as np
import math




def opening_doc(filename, mode):
    # Finds the file to be opened
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)  # Makes the path.
    try:
        numbers = []
        with open(file_path, mode) as file_object:
            for line in file_object:
              number = list(map(int, line.split()))
              numbers.append(number)
        return numbers
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def calc_angle(x, y):
 #calculates angle to of similarity between two vectors.
    
 norm_x = np.linalg.norm(x)
 norm_y = np.linalg.norm(y)
 cos_theta = np.dot(x, y) / (norm_x * norm_y)
 theta = math.degrees(math.acos(cos_theta))
 return theta






def get_Customer_ID():
    customer_ID = []
    data = opening_doc("history.txt" , "r")
    for sublist in data:
       if len(sublist) == 2:  # Check if sublist has exactly two items
                   customer_ID.append(sublist[0])    # Get the first item
    return customer_ID

def get_Item_ID():
    item_ID = []
    data = opening_doc("history.txt" , "r")
    for sublist in data:
       if len(sublist) == 2:  # Check if sublist has exactly two items
             item_ID.append(sublist[-1])  # Get the last item
    return item_ID

def customer_History():
    # Get the list of customer IDs and item IDs
    Cust_ID = get_Customer_ID()  
    item_ID = get_Item_ID()      
    total_ = []
    # Get rid of duplicates and sort the list
    unique_customers = sorted(set(Cust_ID))
    customer_index = {cust: idx for idx, cust in enumerate(unique_customers)}
    # Dictionary to store item vectors (key: item, value: list of 0s and 1s)
    item_Vectors = {}
    # Iterate over both customer IDs and item IDs simultaneously
    for customer, item in zip(Cust_ID, item_ID):
        if item not in item_Vectors:
            # Initialize a zero vector for each item with length equal to unique customers
            item_Vectors[item] = [0] * len(unique_customers)
        # Mark the position corresponding to the customer as 1
        item_Vectors[item][customer_index[customer]] = 1
    # return the item vectors in sorted order
    for key in sorted(item_Vectors.keys()):
        total_.append(item_Vectors[key])
    return total_


def calc_all_angles():
    vector = customer_History()  
    vectors = []
    dic_all_angles = {}

    # Store vectors properly
    for i in range(len(vector)):
        vectors.append(vector[i])

    # Compute angles between each pair of vectors
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):  # Avoid duplicate comparisons
            norm_x = np.linalg.norm(vectors[i])
            norm_y = np.linalg.norm(vectors[j])

            if norm_x == 0 or norm_y == 0:  # Avoid division by zero
                continue

            cos_theta = np.dot(vectors[i], vectors[j]) / (norm_x * norm_y)
            theta = math.degrees(math.acos(np.clip(cos_theta, -1, 1)))  # Ensure input is within valid limits 

            dic_all_angles[f"Vector {i+1} & Vector {j+1}"] = theta

    return dic_all_angles  # Return the dictionary of angles
            
def positive_count():
     
     count = 0
     history = customer_History()

     for i in history:
        
          count += np.count_nonzero(i)

     print(f"Positive entries: {count}")

positive_count()
               
def average_angle():
    vectors = customer_History()
    total = 0
    count = 0  
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):  # Avoid duplicate calculations
            angle = calc_angle(vectors[i], vectors[j])
            total += angle
            count += 1  # Increment count for each valid calculation
    if count == 0:  # Avoid division by zero
        print("No valid angles to compute.")
        return
    average = total / count
    print(f"Average angle: {average:.2f}")

average_angle()
     
def queries():
     query = []

     single_query = []
     Shopping_basketts = (opening_doc("queries.txt" ,"r"))
     #reads queries.txt

     for line in Shopping_basketts:
        query.append(line)
    #appends queries.txt to list

     return query

def check_vector_difference():
    vectors = calc_all_angles()


   
    vector_index -= 1  # Convert to 0-based index for, makes easier on the mind
    if vector_index < 0 or vector_index >= len(vectors):
        return f"Invalid vector index: {vector_index + 1}"

    angles_with_selected = {}

    for j in range(len(vectors)):
        if j == vector_index:
            continue  # Avoids self comparison

        norm_x = np.linalg.norm(vectors[vector_index])
        norm_y = np.linalg.norm(vectors[j])

        if norm_x == 0 or norm_y == 0:  # Avoid division by zero
            continue

        cos_theta = np.dot(vectors[vector_index], vectors[j]) / (norm_x * norm_y)
        theta = math.degrees(math.acos(np.clip(cos_theta, -1, 1)))  #Makes sure input is valid.

        angles_with_selected[f"Vector {vector_index+1} & Vector {j+1}"] = theta

    return angles_with_selected  # Return angles between the selected vector and others




def process_queries():
    # Get vectors from customer history
    vectors = customer_History()
    
    # Ensure we have valid data
    if not vectors:
        print("Error: No customer history data available.")
        return
    
    # Get queries from queries.txt
    query_lines = queries()

    if not query_lines:
        print("Error: No query data available.")
        return

    # Process each line of queries
    for line in query_lines:
        try:
            query_indices = list(map(int, line))  # Convert query to list of integers
        except ValueError:
            print(f"Invalid query format: {line}")
            continue  # Skip invalid lines

        print("Shopping cart:", " ".join(map(str, query_indices)))
        #prints whats in query line (the shopping cart)


        recommend = []

        # Process each index from the line
        for vector_index in query_indices:
            if not (1 <= vector_index <= len(vectors)):  # Validate index
                print(f"Invalid vector index: {vector_index}")
                continue

            min_angle = float('inf')
            min_vector = None

            # Calculate angles between the queried vector and all others
            for j in range(len(vectors)):
                if j == vector_index - 1:  # Skip comparing the same vector
                    continue

                # Calculate the angle
                angle = calc_angle(vectors[vector_index - 1], vectors[j])


                # Update minimum angle and vector index if the angle is less than the current angle (minimum)
                if angle < min_angle:
                    min_angle = angle
                    min_vector = j + 1  # Convert back to 1-based index for computer

            # Print the result for the current query
            if min_vector is not None and min_angle < 90:  # Match found if the angle is less than 90
                print(f"Item: {vector_index}; match: {min_vector}; angle: {min_angle:.2f}")
                recommend.append(str(min_vector))
            else:
                print(f"Item {vector_index} no match")

        # Print the final recommendation list
        if recommend:
            print("Recommend:", " ".join(sorted(set(recommend))))
        else:
            print("Recommend:")  



def printin():
    positive_count()
    average_angle()
    process_queries()
    queries()


printin()




