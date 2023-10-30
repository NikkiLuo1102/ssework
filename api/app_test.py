from app import process_query


def test_knows_about_dinosaurs():
    st1 = "Dinosaurs ruled the Earth 200 million years ago"
    assert process_query("dinosaurs") == st1


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"

def tests_knows_about_my_name():
    assert process_query("What is your name?") == "KFC V50"