""" Helper functions ot be used by all tests """


def metadata():
    return {'key': 'value'}


def metadata_with_filtered_data():
    return {'key': 'value', 'key1': 'value1', 'key2': 'value2'}


def violations():
    return [
        {
            "description": "Privileged container: hello-octarine (CIS 1.7.1)",
            "violation_category": "SecurityContext",
            "violation_name": "privileged-container"
        },
        {
            "description": "Share host network container: hello-octarine (CIS 1.7.4)",
            "violation_category": "SecurityContext",
            "violation_name": "share-host-network-container"
        },
        {
            "description": "container hello-octarine capability added: CAP_SYS_ADMIN",
            "violation_category": "SecurityContext",
            "violation_name": "container-sys-admin-cap-added"
        }
    ]


def key():
    return "Kind:Name:Namespace"


def keys():
    return ["Kind{}:Name{}".format(x, x) for x in range(5)]
