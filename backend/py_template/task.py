from flask import Flask, request
from typing import List, Dict
from utils import Utils


# ==== DO NOT CHANGE ==========================================================
app = Flask(__name__)

# ==== Type Definitions, feel free to add or modify ===========================
project_registry: Dict[str, Dict] = {}

class Slug:
    def __init__(self, slug: str):
        self._slug = slug

    @property
    def slug(self):
        return self._slug

class RequiredResource:
    def __init__(self,name,quantity):
        self.name = name
        self.quantity = quantity
    
    def __repr__(self):
        return f"Name: {self.name}, Quantity: {self.quantity}"

class ProjectEntry:
    def __init__(self, name: str, requiredResources: List[RequiredResource]):
        self.type = "project"
        self.name = name
        self.requiredResources = requiredResources
    
    def __str__(self):
        return f"Project, Name: {self.name}, Required Resources: {self.requiredResources}"

class ResourceEntry:
    def __init__(self, name: str, buildTime: int):
        self.type = "resource"
        self.name = name
        self.buildTime = buildTime

    def __str__(self):
        return f"Project, Name: {self.name}, Build Time: {self.buildTime}"

# ==== Task 1 =================================================================
@app.route("/slugToTitle", methods=["GET"])
def slug_to_title():
    if request.args.get("slug") == None:
        return "",200
    slug = Slug(request.args.get("slug"))
    title = Utils.slug_to_title(slug)
    return title, 200

# ==== Task 2 =================================================================
@app.route("/projectEntry", methods=["POST"])
def add_project_entry():
    # Mock registry
    registryData = [ProjectEntry("test1",[RequiredResource("req1",10)]),ProjectEntry("test2",[RequiredResource("req1",10)]),]
    project_names = [project.name for project in registryData]

    data = request.get_json()

    name = data.get("name")
    if name in project_names:
        return f"Project with name: {name},already exits in registry",400
    type = data.get("type")
    if type != "project" and type != "resource":
        return "Entry type must match either project or resource",422
    if type == "project":
        if "requiredResources" not in data.keys():
            return "requiredResources is required",400
        requiredResources = data.get("requiredResources")
        if len(requiredResources) == 0 or requiredResources == None:
            return "At least one requiredResources (int) is needed", 400
        else:
            try:
                requiredResources = [RequiredResource(resource.get("name"),resource.get("quantity")) for resource in requiredResources]
                resources_names = [resource.name for resource in requiredResources]
                if len(set(resources_names)) != len(resources_names):
                    return "Duplicate resource names are not allowed",400
                project_entry = ProjectEntry(name,requiredResources=requiredResources)
                # Add to DB
                return str(project_entry),200
            except:
                return "RequiredResource must have a name and quantity", 400
    else:
        if "buildTime" not in data.keys():
            return "buildTime is required",400
        buildTime = data.get("buildTime")
        if buildTime == None:
            return "buildTime(int) is required for resource entry", 400
        else:
            try:
                buildTime = int(buildTime)
            except:
                return "buildTime must be an int", 400
            if buildTime < 0:
                return "buildTime must be greater than or equal to zero", 400
            resource_entry = ResourceEntry(name,buildTime=buildTime)
            return str(resource_entry),200
            



# ==== Task 3 =================================================================
@app.route("/summary", methods=["GET"])
def get_summary():
    name = request.args.get("name")
    # TODO: Lookup entry and compute total build time and base resources
    return "", 200


# ==== DO NOT CHANGE ==========================================================
if __name__ == "__main__":
    app.run(debug=True, port=8080)
