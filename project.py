from kubernetes import client, config
from kubernetes.client import V1Pod, V1PodSpec, V1Container, V1ObjectMeta

# Load Kubernetes configuration
config.load_kube_config()

# Create an API client
api_instance = client.CoreV1Api()

# Define the pod specification
pod = V1Pod(
    metadata=V1ObjectMeta(name="example-pod"),
    spec=V1PodSpec(
        containers=[V1Container(
            name="example-container",
            image="busybox",
            command=["/bin/sh", "-c", "echo Hello Kubernetes! && sleep 30"]
        )]
    )
)

def create_pod(api_instance, pod):
    try:
        api_response = api_instance.create_namespaced_pod(
            namespace="default",
            body=pod
        )
        print(f"Pod created. Status: {api_response.status.phase}")
    except client.exceptions.ApiException as e:
        print(f"Exception when creating pod: {e}")

def get_pod_status(api_instance, pod_name):
    try:
        api_response = api_instance.read_namespaced_pod_status(
            name=pod_name,
            namespace="default"
        )
        return api_response.status.phase
    except client.exceptions.ApiException as e:
        print(f"Exception when reading pod status: {e}")

def delete_pod(api_instance, pod_name):
    try:
        api_response = api_instance.delete_namespaced_pod(
            name=pod_name,
            namespace="default",
            body=client.V1DeleteOptions()
        )
        print(f"Pod deleted. Status: {api_response.status}")
    except client.exceptions.ApiException as e:
        print(f"Exception when deleting pod: {e}")

if __name__ == "__main__":
    # Create the pod
    create_pod(api_instance, pod)

    # Wait for the pod to complete its job
    import time
    while True:
        status = get_pod_status(api_instance, "example-pod")
        print(f"Pod status: {status}")
        if status in ["Succeeded", "Failed"]:
            break
        time.sleep(5)

    # Delete the pod once it's done
    delete_pod(api_instance, "example-pod")
