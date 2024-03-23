import tkinter as tk
import random
import math

class ClosestPairFinderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Closest Pair Finder")

        self.points = []

        # Canvas dimensions
        self.canvas_width = 1000
        self.canvas_height = 500

        # Labels
        self.label_instruction = tk.Label(master, text="Enter 2D Points (x, y):")
        self.label_instruction.pack()

        # Entry for points
        self.entry_points = tk.Entry(master, width=30)
        self.entry_points.pack()

        # Button to add points
        self.button_add_point = tk.Button(master, text="Add Point", command=self.add_point)
        self.button_add_point.pack()

        # Button to generate random points
        self.button_generate_random_points = tk.Button(master, text="Generate Random Points", command=self.generate_random_points)
        self.button_generate_random_points.pack()

        # Canvas for visualization
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Button to find closest pair
        self.button_find_closest_pair = tk.Button(master, text="Find Closest Pair", command=self.find_closest_pair)
        self.button_find_closest_pair.pack()

    def add_point(self):
        try:
            # Get the entered point as a tuple (x, y)
            point_str = self.entry_points.get()
            x, y = map(float, point_str.split(","))

            # Ensure the point is within the canvas bounds
            if 0 <= x <= self.canvas_width and 0 <= y <= self.canvas_height:
                self.points.append((x, y))
                print("Input points:", "(",x,",",y,")")
                # Display the added point on canvas
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

                # Clear the entry field
                self.entry_points.delete(0, tk.END)
            else:
                print("Point is outside the canvas bounds.")

        except ValueError:
            print("Invalid input. Please enter points in the format 'x, y'.")

    def generate_random_points(self):
        # Clear previous points on canvas and the self.points list
        self.canvas.delete("all")
        self.points = []

        # Generate a random number of points (between 5 and 20)
        num_points = random.randint(5, 20)

        for _ in range(num_points):
            x = random.uniform(3, self.canvas_width - 3)
            y = random.uniform(3, self.canvas_height - 3)

            self.points.append((x, y))

            # Display the random points on canvas
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")
        print("Random Points:", self.points)

    def find_closest_pair(self):
        if len(self.points) < 2:
            print("Insufficient points to find the closest pair.")
            return

        def euclidean_distance(point1, point2):
            return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

        def closest_pair_bruteforce(points):
            min_distance = float('inf')
            closest_pair = None

            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    distance = euclidean_distance(points[i], points[j])
                    if distance < min_distance:
                        min_distance = distance
                        closest_pair = (points[i], points[j])

            return closest_pair, min_distance

        def closest_pair_divide_conquer(points):
            if len(points) <= 3:
                return closest_pair_bruteforce(points)

            sorted_points = sorted(points, key=lambda x: x[0])
            mid = len(sorted_points) // 2
            left_half = sorted_points[:mid]
            right_half = sorted_points[mid:]

            left_closest, left_distance = closest_pair_divide_conquer(left_half)
            right_closest, right_distance = closest_pair_divide_conquer(right_half)

            if left_distance < right_distance:
                min_distance = left_distance
                closest_pair = left_closest
            else:
                min_distance = right_distance
                closest_pair = right_closest

            mid_x = (sorted_points[mid - 1][0] + sorted_points[mid][0]) / 2
            candidates = [point for point in sorted_points if abs(point[0] - mid_x) < min_distance]
            candidates.sort(key=lambda x: x[1])

            for i in range(len(candidates)):
                j = i + 1
                while j < len(candidates) and candidates[j][1] - candidates[i][1] < min_distance:
                    distance = euclidean_distance(candidates[i], candidates[j])
                    if distance < min_distance:
                        min_distance = distance
                        closest_pair = (candidates[i], candidates[j])
                    j += 1

            return closest_pair, min_distance



        # Visualize the closest pair
        closest_pair, min_distance = closest_pair_divide_conquer(self.points)
        if closest_pair:
            point1, point2 = closest_pair
            x1, y1 = point1
            x2, y2 = point2
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

        print("Closest Pair:", closest_pair)
        print("Minimum Distance:", min_distance)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClosestPairFinderApp(root)
    root.mainloop()
