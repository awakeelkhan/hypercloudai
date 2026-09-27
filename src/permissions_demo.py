from src.core.tool_permissions import ToolPermissions


permissions = ToolPermissions(
    allowedTools=["listDirectory", "searchProject", "deleteFile"],
    deniedTools=["formatDisk"],
    readOnlyTools=["listDirectory", "searchProject"],
    actionTools=["deleteFile", "formatDisk"]
)

print("listDirectory allowed:", permissions.isAllowed("listDirectory"))
print("listDirectory read-only:", permissions.isReadOnly("listDirectory"))

print("formatDisk allowed:", permissions.isAllowed("formatDisk"))
print("formatDisk action:", permissions.isAction("formatDisk"))

print("deleteFile:")
print("Approved:", permissions.approve("deleteFile"))