from manim import *
import numpy as np

###### manim -pql -qh pres.py FruitClassification ######

class FruitClassification(Scene):
    def construct(self):
        # Define colorblind-friendly colors
        COLOR_1 = "#1b9e77"  # Apples
        COLOR_2 = "#d95f02"  # Oranges
        COLOR_3 = "#7570b3"  # Unknown fruit

        # Introductory slides
        # Slide 1: Mystery fruit
        mystery_fruit = Circle(radius=1, color=COLOR_3, fill_opacity=0.5)
        question_mark = Text("?", color=WHITE).scale(2)
        mystery_group = VGroup(mystery_fruit, question_mark)
        
        title = Text("Mystery Fruit", color=WHITE).scale(0.8)
        title.to_edge(UP)
        
        self.play(Create(mystery_fruit), Write(question_mark), Write(title))
        self.wait(2)

        # Slide 2: Known fruits
        apple = Circle(radius=0.5, color=COLOR_1, fill_opacity=0.5)
        orange = Circle(radius=0.5, color=COLOR_2, fill_opacity=0.5)
        apple_text = Text("Apple", color=COLOR_1).scale(0.5).next_to(apple, DOWN)
        orange_text = Text("Orange", color=COLOR_2).scale(0.5).next_to(orange, DOWN)
        
        known_fruits = VGroup(apple, orange, apple_text, orange_text).arrange(RIGHT, buff=1)
        known_fruits.next_to(mystery_group, DOWN, buff=1)
        
        self.play(
            Create(apple),
            Create(orange),
            Write(apple_text),
            Write(orange_text)
        )
        self.wait(2)

        # Slide 3: Comparison
        arrows = VGroup(
            Arrow(start=mystery_fruit.get_bottom(), end=apple.get_top(), color=WHITE),
            Arrow(start=mystery_fruit.get_bottom(), end=orange.get_top(), color=WHITE)
        )
        
        compare_text = Text("Compare", color=WHITE).scale(0.6)
        compare_text.next_to(arrows, RIGHT)
        
        self.play(Create(arrows), Write(compare_text))
        self.wait(2)

        # Clear the introductory slides
        self.play(
            FadeOut(mystery_group),
            FadeOut(known_fruits),
            FadeOut(arrows),
            FadeOut(compare_text),
            FadeOut(title)
        )

        # Main explanation slide
        title = Text("Fruit Classification using K-Nearest Neighbors", color=WHITE).scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))

        explanation = Text("We'll compare our mystery fruit to nearby fruits we already know,", 
                           color=WHITE).scale(0.6)
        explanation2 = Text("based on their size and color.", color=WHITE).scale(0.6)
        explanation.next_to(title, DOWN, buff=0.5)
        explanation2.next_to(explanation, DOWN, buff=0.2)
        self.play(Write(explanation), Write(explanation2))
        self.wait(3)

        # Clear the explanation slide
        self.play(FadeOut(title), FadeOut(explanation), FadeOut(explanation2))

        # Function to get random point within the chart
        def get_random_point():
            x = np.random.uniform(0, 10)
            y = np.random.uniform(0, 10)
            return chart.c2p(x, y)
        
        # Set up the fruit chart (size vs. color)
        chart = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"color": WHITE},
            tips=False,
        )
        chart_title = Text("Fruit Classification Chart", color=WHITE).scale(0.8)
        chart_title.to_edge(UP)

        # Create and position axis labels
        x_label = Text("Size", color=WHITE).scale(0.5)
        y_label = Text("Color (Redness)", color=WHITE).scale(0.5)
        x_label.next_to(chart.x_axis, DOWN)
        y_label.next_to(chart.y_axis, LEFT).rotate(90 * DEGREES)

        # Add chart and labels to the scene
        self.play(Create(chart), Write(chart_title))
        self.play(Write(x_label), Write(y_label))

        # Create fruits (data points)
        apples = VGroup(*[Dot(color=COLOR_1).move_to(chart.c2p(np.random.uniform(0, 10), np.random.uniform(0, 10))) for _ in range(15)])
        oranges = VGroup(*[Dot(color=COLOR_2).move_to(chart.c2p(np.random.uniform(0, 10), np.random.uniform(0, 10))) for _ in range(15)])

        self.play(Create(apples), Create(oranges), run_time=2)

        # Add labels for apples and oranges
        apple_label = Text("Apples", color=COLOR_1).scale(0.5)
        orange_label = Text("Oranges", color=COLOR_2).scale(0.5)
        legend = VGroup(apple_label, orange_label).arrange(RIGHT, buff=0.5)
        legend.to_corner(UR)
        self.play(Write(legend), run_time=1)


        # New fruit (point to classify)
        new_fruit = Dot(color=COLOR_3).move_to(get_random_point())
        new_fruit_label = Text("Mystery Fruit", color=COLOR_3).scale(0.5).next_to(new_fruit, DOWN)
        self.play(Create(new_fruit), Write(new_fruit_label), run_time=1)

        # Find K nearest neighbors (K=3)
        k = 3
        all_fruits = list(apples) + list(oranges)
        distances = [np.linalg.norm(fruit.get_center() - new_fruit.get_center()) for fruit in all_fruits]
        nearest_indices = sorted(range(len(distances)), key=lambda i: distances[i])[:k]

        # Highlight nearest neighbors
        circles = VGroup(*[Circle(radius=0.3, color=COLOR_3).move_to(all_fruits[i].get_center()) 
                           for i in nearest_indices])
        self.play(Create(circles), run_time=2)

        # Count votes
        apple_votes = sum(1 for i in nearest_indices if i < len(apples))
        orange_votes = k - apple_votes

        # Show decision
        if apple_votes > orange_votes:
            decision = Text("Mystery fruit is likely an Apple!", color=COLOR_3).scale(0.7)
        else:
            decision = Text("Mystery fruit is likely an Orange!", color=COLOR_3).scale(0.7)
        decision.to_edge(DOWN)
        self.play(Write(decision), run_time=1)

        # Add a pause for emphasis
        self.wait(2)

        # Add a fun animation to show the decision
        if apple_votes > orange_votes:
            self.play(new_fruit.animate.set_color(COLOR_1).scale(1.2), run_time=1)
        else:
            self.play(new_fruit.animate.set_color(COLOR_2).scale(1.2), run_time=1)

        # Final pause
        self.wait(2)


###### manim -pql -qh pres.py KNNVisualization ######

class KNNVisualization(Scene):
    def construct(self):
        self.color_coding()
        self.introduce_method()
        self.show_data_points()
        self.demonstrate_euclidean_distance()
        self.calculate_distances()
        self.find_k_nearest()
        self.retrieve_labels()
        self.make_prediction()
        self.conclusion()

    def color_coding(self):
        self.code_color = "#E6E6E6"  # Light gray for code
        self.highlight_color = "#FFA500"  # Orange for highlights
        self.point_color = "#4363d8"  # Blue for data points
        self.new_point_color = "#e6194B"  # Red for new point
        self.text_color = "#FFFFFF"  # White for text

    def introduce_method(self):
        title = Text("KNN: _predict_single Method", font_size=40, color=self.text_color)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

    def show_data_points(self):
        code = Code(
            code="""
            def _predict_single(self, observation):
                # Step 1: Prepare data
                X = self._parameters["observations"]
                y = self._parameters["ground_truth"]
            """,
            language="python",
            font_size=24,
            background="window",
            background_stroke_width=1,
            background_stroke_color=self.code_color,
        )
        self.play(Create(code))
        self.wait(2)

        # Create a scatter plot of training data
        ax = Axes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            axis_config={"color": self.text_color},
        )
        dots = VGroup(*[Dot(ax.c2p(np.random.uniform(-4, 4), np.random.uniform(-4, 4)), color=self.point_color) for _ in range(20)])
        new_point = Dot(ax.c2p(2, 2), color=self.new_point_color)
        
        self.play(FadeOut(code))
        self.play(Create(ax), Create(dots), Create(new_point))
        
        label = Text("Training points (blue) and new point (red)", font_size=24, color=self.text_color).next_to(ax, DOWN)
        self.play(Write(label))
        self.wait(2)
        self.play(FadeOut(label))

        # Store these for later use
        self.ax = ax
        self.dots = dots
        self.new_point = new_point

    def demonstrate_euclidean_distance(self):
        # Clear previous objects
        self.play(FadeOut(self.ax), FadeOut(self.dots), FadeOut(self.new_point))

        # Create two points
        ax = Axes(
            x_range=[-1, 6],
            y_range=[-1, 6],
            axis_config={"color": self.text_color},
        )
        point1 = Dot(ax.c2p(1, 1), color=self.point_color)
        point2 = Dot(ax.c2p(4, 5), color=self.new_point_color)

        # Draw line between points
        line = Line(point1.get_center(), point2.get_center(), color=self.highlight_color)

        # Label points
        label1 = Text("A (1, 1)", font_size=20, color=self.text_color).next_to(point1, DOWN)
        label2 = Text("B (4, 5)", font_size=20, color=self.text_color).next_to(point2, UP)

        # Euclidean distance formula
        formula = Text(r"\text{distance}^2 = (x_2-x_1)^2 + (y_2-y_1)^2", color=self.text_color).to_edge(UP)

        # Calculate distance
        distance_squared = (4-1)**2 + (5-1)**2
        result = Text(f"Distance² = {distance_squared}", font_size=24, color=self.highlight_color).next_to(formula, DOWN)
        final_result = Text(f"Distance ≈ {np.sqrt(distance_squared):.2f}", font_size=24, color=self.highlight_color).next_to(result, DOWN)

        self.play(Create(ax), Create(point1), Create(point2), Create(label1), Create(label2))
        self.play(Create(line))
        self.play(Write(formula))
        self.play(Write(result))
        self.play(Write(final_result))
        self.wait(2)

        self.play(FadeOut(ax), FadeOut(point1), FadeOut(point2), FadeOut(label1), FadeOut(label2),
                  FadeOut(line), FadeOut(formula), FadeOut(result), FadeOut(final_result))

        # Bring back original plot
        self.play(FadeIn(self.ax), FadeIn(self.dots), FadeIn(self.new_point))

    def find_k_nearest(self):
        code = Code(
            code="""
                # Step 3: Find k nearest neighbors
                k_indices = np.argsort(distances)[:self.k]
            """,
            language="python",
            font_size=24,
            background="window",
            background_stroke_width=1,
            background_stroke_color=self.code_color,
        )
        self.play(Create(code))
        self.wait(2)
        self.play(FadeOut(code))

        # Visualize array sorting and slicing
        distances = [3.1, 2.7, 5.2, 1.4, 4.8, 3.6, 2.3, 6.1]
        sorted_indices = np.argsort(distances)
        k = 3

        # Create unsorted array visualization
        unsorted_array_viz = VGroup(*[Square(side_length=0.5, fill_opacity=0.5, fill_color=self.point_color) for _ in range(len(distances))])
        unsorted_array_viz.arrange(RIGHT, buff=0.1)
        unsorted_array_labels = VGroup(*[Text(f"{d:.1f}", font_size=16, color=self.text_color) for d in distances])
        for label, square in zip(unsorted_array_labels, unsorted_array_viz):
            label.move_to(square.get_center())

        self.play(Create(unsorted_array_viz), Write(unsorted_array_labels))
        self.wait(1)

        # Create sorted array visualization
        sorted_array_viz = VGroup(*[Square(side_length=0.5, fill_opacity=0.5, fill_color=self.point_color) for _ in range(len(distances))])
        sorted_array_viz.arrange(RIGHT, buff=0.1).next_to(unsorted_array_viz, DOWN, buff=0.5)
        sorted_array_labels = VGroup(*[Text(f"{distances[i]:.1f}", font_size=16, color=self.text_color) for i in sorted_indices])
        for label, square in zip(sorted_array_labels, sorted_array_viz):
            label.move_to(square.get_center())

        self.play(
            ReplacementTransform(unsorted_array_viz, sorted_array_viz),
            ReplacementTransform(unsorted_array_labels, sorted_array_labels)
        )
        self.wait(1)

        # Show k-nearest selection
        brace = Brace(sorted_array_viz[:k], DOWN, color=self.highlight_color)
        brace_label = Text(f"k={k}", font_size=24, color=self.highlight_color).next_to(brace, DOWN)

        self.play(Create(brace), Write(brace_label))
        self.wait(2)

        self.play(FadeOut(sorted_array_viz), FadeOut(sorted_array_labels), FadeOut(brace), FadeOut(brace_label))

        # Highlight k nearest neighbors
        k = 3
        distances = [np.linalg.norm(np.array(dot.get_center()) - np.array(self.new_point.get_center())) for dot in self.dots]
        self.k_nearest = sorted(zip(distances, self.dots))[:k]
        
        highlight = VGroup(*[Circle(color=self.highlight_color).surround(dot) for _, dot in self.k_nearest])
        self.play(Create(highlight))
        
        label = Text(f"Find {k} nearest neighbors", font_size=24, color=self.text_color).next_to(self.ax, DOWN)
        self.play(Write(label))
        self.wait(2)
        self.play(FadeOut(label))
        
        # Store the highlight for later use
        self.k_nearest_highlight = highlight

    def calculate_distances(self):
        code = Code(
            code="""
                # Step 2: Calculate distances
                distances = np.linalg.norm(X - observation, axis=1)
            """,
            language="python",
            font_size=24,
            background="window",
            background_stroke_width=1,
            background_stroke_color=self.code_color,
        )
        self.play(Create(code))
        self.wait(2)
        self.play(FadeOut(code))

        # Visualize distance calculation
        lines = VGroup(*[Line(self.new_point.get_center(), dot.get_center(), color=self.highlight_color) for dot in self.dots])
        self.play(Create(lines))
        
        label = Text("Calculate distances to all training points", font_size=24, color=self.text_color).next_to(self.ax, DOWN)
        self.play(Write(label))
        self.wait(2)
        self.play(FadeOut(label), FadeOut(lines))

    def retrieve_labels(self):
        code = Code(
            code="""
                # Step 4: Retrieve labels of nearest neighbors
                k_nearest_labels = y[k_indices]
            """,
            language="python",
            font_size=24,
            background="window",
            background_stroke_width=1,
            background_stroke_color=self.code_color,
        )
        self.play(Create(code))
        self.wait(2)
        self.play(FadeOut(code))

        # Show labels of nearest neighbors
        labels = VGroup(*[Text(str(i+1), font_size=20, color=self.text_color).next_to(dot, UP) for i, (_, dot) in enumerate(self.k_nearest)])
        
        self.play(Create(labels))
        
        label = Text("Retrieve labels of nearest neighbors", font_size=24, color=self.text_color).next_to(self.ax, DOWN)
        self.play(Write(label))
        self.wait(2)
        self.play(FadeOut(label), FadeOut(labels))

    def make_prediction(self):
        code = Code(
            code="""
                # Step 5: Make prediction
                most_common = Counter(k_nearest_labels).most_common(1)
                return most_common[0][0]
            """,
            language="python",
            font_size=24,
            background="window",
            background_stroke_width=1,
            background_stroke_color=self.code_color,
        )
        self.play(Create(code))
        self.wait(2)
        self.play(FadeOut(code))

        # Visualize voting process
        labels = np.random.choice([1, 2, 3], size=3)
        vote_count = Text(f"Votes: {', '.join(map(str, labels))}", font_size=24, color=self.text_color).next_to(self.ax, DOWN)
        prediction = Text(f"Prediction: {np.bincount(labels).argmax()}", font_size=24, color=self.highlight_color).next_to(vote_count, DOWN)
        
        self.play(Write(vote_count))
        self.wait(1)
        self.play(Write(prediction))
        self.wait(2)
        self.play(FadeOut(vote_count), FadeOut(prediction))
        
        # Clean up
        self.play(FadeOut(self.k_nearest_highlight))

    def conclusion(self):
        conclusion = Text("KNN predicts brased on majority vote of nearest neighbors", font_size=30, color=self.text_color)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))
