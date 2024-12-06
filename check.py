import pkg_resources
import os

# Get the list of installed packages and their sizes
packages = [
    (dist.project_name, dist.location)
    for dist in pkg_resources.working_set
]

# Calculate sizes and sort
sizes = []
for package, location in packages:
    try:
        # Get package size by summing file sizes in the package directory
        total_size = sum(
            os.path.getsize(os.path.join(root, file))
            for root, _, files in os.walk(location)
            for file in files
        )
        sizes.append((package, total_size))
    except Exception as e:
        continue  # Ignore errors

# Sort by size in descending order
sorted_packages = sorted(sizes, key=lambda x: x[1], reverse=True)


# Display the results
for package, size in sorted_packages:
    print(f"{package}: {size / (1024**2):.2f} MB")
