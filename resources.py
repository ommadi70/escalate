# resources.py

# This dictionary represents the finite shared resources in your cluster.
# This is what causes bottlenecks if a standard reactive scheduler is used.
RESOURCES = {
    "LLM": 3,
    "GPU": 1,
    "Database": 2,
    "Search": 5,
    "Python": 2,
    "Storage": 4,
    "PDF": 1
}

def get_initial_resources():
    """Returns a fresh copy of the resource pool."""
    return dict(RESOURCES)