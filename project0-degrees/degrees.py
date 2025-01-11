import csv
import sys
from collections import defaultdict

from util import Node, StackFrontier, QueueFrontier

sys.setrecursionlimit(1000000)

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Use defaultdict for automatic handling of missing keys
    people = {}
    names = {}
    movies = {}

    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

    return people, names, movies


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")

    people, names, movies = load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "), names, people)
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "), names, people)
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target, people, movies)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target, people, movies):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier().add(start)

    # Create an immutable set to store the explored nodes
    explored = frozenset()

    def find_solution(frontier, explored):
        if frontier.empty():
            return None

        node, new_frontier = frontier.remove()
        if node.state == target:
            # Reconstruct path
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        new_explored = explored | frozenset([node.state])

        def add_neighbors(frontier, neighbors, explored):
            next_neighbor = next(neighbors, None)
            if next_neighbor is None:
                return None, frontier

            movie_id, person_id = next_neighbor

            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)

                # If child is the target, then we have a solution
                if child.state == target:
                    path = []
                    while child.parent is not None:
                        path.append((child.action, child.state))
                        child = child.parent
                    path.reverse()
                    return path, None

                frontier = frontier.add(child)

            return add_neighbors(frontier, neighbors, explored)

        solution, new_frontier = add_neighbors(new_frontier, neighbors_for_person(node.state, people, movies), new_explored)
        if solution is not None:
            return solution

        return find_solution(new_frontier, new_explored)

    return find_solution(frontier, explored)


def person_id_for_name(name, names, people):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id, people, movies):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    return (
        (movie_id, person_id)
        for movie_id in movie_ids
        for person_id in movies[movie_id]["stars"]
    )


if __name__ == "__main__":
    main()
