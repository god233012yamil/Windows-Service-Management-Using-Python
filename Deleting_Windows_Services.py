import win32service
import win32serviceutil

def delete_service(service_name: str) -> None:
    """
    Delete the specified Windows service.

    Parameters
    ----------
    service_name : str
        The name of the service to delete.

    Returns
    -------
    None
    """
    try:
        # Open a handle to the service control manager
        scm = win32service.OpenSCManager(None, None, 
                                         win32service.SC_MANAGER_ALL_ACCESS)
        # Open the service with all access
        service = win32service.OpenService(scm, service_name, 
                                           win32service.SERVICE_ALL_ACCESS)

        # Stop the service if it is running
        try:
            win32serviceutil.StopService(service_name)
        except Exception as e:
            print(f"Service '{service_name}' may not be running or 
                  could not be stopped: {e}")

        # Delete the service
        win32service.DeleteService(service)
        print(f"Service '{service_name}' deleted successfully.")
        
        # Close the service handle
        win32service.CloseServiceHandle(service)
        # Close the service control manager handle
        win32service.CloseServiceHandle(scm)
    except Exception as e:
        print(f"Failed to delete service '{service_name}': {e}")

if __name__ == "__main__":
    # Example usage
    service_name = "MyPythonService"
    delete_service(service_name)
