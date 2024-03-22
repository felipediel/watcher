## Questions

After completing your implementation, you should include a write up that answers the following questions:

1. Discuss your strategy and decisions implementing the application. Please, consider time complexity, effort cost, technologies used and any other variable that you understand important on your development process.

I chose Python and Django primarily due to their advantages in terms of fast development and robust ecosystem.

In implementing the application with the repository pattern, I focused on modularity and flexibility. By utilizing repositories for data access and default_storage for file handling, I aimed to decouple the application logic from specific data storage implementations, promoting code maintainability and extensibility.

The current design ensures that if there's a future decision to migrate the data to a relational database for improved performance, transitioning would be straightforward. By creating SQL repository classes that mirror the interface of the existing CSV repositories, we can seamlessly switch between data storage implementations without requiring changes to the application logic. This flexibility allows us to adapt to evolving requirements and scale the application as needed, ensuring its long-term viability and maintainability.

Moreover, the use of the specification pattern complements the repository pattern by providing a flexible and modular approach to data filtering. By encapsulating filtering criteria within specification objects, we decouple the filtering logic from the repositories, views, and other parts of the application. This separation of concerns enhances maintainability, as changes to filtering requirements can be implemented independently of other components.

2. How would you change your solution to account forfuture columns that might be requested, such as “Bill Voted On Date” or “Co-Sponsors”?

Firstly I'd augment the existing data models by adding new fields to represent the additional columns. Next I would update the 'build_item()' method in the repository classes to handle the parsing of these new fields from storage. Then I would extend the 'search_fields' and 'get_query_params()' in the views, incorporating these new fields into the search filters. Lastly, I would modify the frontend to display the fields as requested.

To streamline this process, I could consider implementing dataclass inspectors to read from and write to CSV columns based on properties. These inspectors can facilitate the mapping of data fields to CSV columns, simplifying the data retrieval and storage process. There is a python library named 'dataclass-csv' that I could use.

3. How would you change your solution if instead of receiving CSVs of data, you were given a list of legislators or bills that you should generate a CSV for?

I would create a DataclassToCsvWriter class with this signature:

```python3
import io
from typing import TypeVar

T = TypeVar("T")

class DataclassToCsvWriter(Generic[T]):
    def __init__(self, file: io.TextIOBase, obj_list: list[T], obj_type: type[T]) -> None:
        """Initialize CSV writer."""

    def write() -> None:
        """Write data to file."""
```

This class would be responsible for inspecting the dataclass properties and mapping them to columns in the CSV file. With this class in place, it can be instantiated and called within the view with the relevant data. The resulting files can then be saved to the default storage and the file address can be returned to the user.

4. How long did you spend working on the assignment?

I dedicated approximately 3 hours to build a functional version. Then I've spent 2 days refining the design, adding search filters, creating unit tests, improving the frontend and documenting the application.
