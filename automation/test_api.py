import requests


BASE_URL = "http://127.0.0.1:5000"
API_KEY = "ctap2310-devnet-key"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def print_result(test_name, passed, status_code=None):
    if passed:
        print(f"PASS - {test_name}")
    else:
        print(f"FAIL - {test_name} - Status: {status_code}")


def test_authenticated_get():
    response = requests.get(
        f"{BASE_URL}/devices",
        headers=HEADERS
    )

    print_result(
        "Authenticated GET /devices",
        response.status_code == 200,
        response.status_code
    )


def test_unauthorised_get():
    response = requests.get(
        f"{BASE_URL}/devices"
    )

    print_result(
        "Unauthorised GET /devices",
        response.status_code == 401,
        response.status_code
    )


def test_device_not_found():
    response = requests.get(
        f"{BASE_URL}/devices/DOES-NOT-EXIST",
        headers=HEADERS
    )

    print_result(
        "GET nonexistent device",
        response.status_code == 404,
        response.status_code
    )


def test_create_device():
    payload = {
        "environment": "office",
        "hostname": "PYTHON-TEST-R1",
        "vendor": "Cisco",
        "ip_address": "192.168.60.1",
        "role": "Python Test Router"
    }

    response = requests.post(
        f"{BASE_URL}/devices",
        headers=HEADERS,
        json=payload
    )

    print_result(
        "POST create device",
        response.status_code == 201,
        response.status_code
    )


def test_duplicate_device():
    payload = {
        "environment": "office",
        "hostname": "PYTHON-TEST-R1",
        "vendor": "Cisco",
        "ip_address": "192.168.60.1",
        "role": "Python Test Router"
    }

    response = requests.post(
        f"{BASE_URL}/devices",
        headers=HEADERS,
        json=payload
    )

    print_result(
        "POST duplicate device",
        response.status_code == 409,
        response.status_code
    )


def test_invalid_ip():
    payload = {
        "environment": "office",
        "hostname": "PYTHON-TEST-R2",
        "vendor": "Cisco",
        "ip_address": "999.999.999.999",
        "role": "Invalid Router"
    }

    response = requests.post(
        f"{BASE_URL}/devices",
        headers=HEADERS,
        json=payload
    )

    print_result(
        "POST invalid IP address",
        response.status_code == 400,
        response.status_code
    )


def test_update_device():
    payload = {
        "ip_address": "192.168.60.10",
        "role": "Updated Python Test Router"
    }

    response = requests.put(
        f"{BASE_URL}/devices/PYTHON-TEST-R1",
        headers=HEADERS,
        json=payload
    )

    print_result(
        "PUT update device",
        response.status_code == 200,
        response.status_code
    )


def test_delete_device():
    response = requests.delete(
        f"{BASE_URL}/devices/PYTHON-TEST-R1",
        headers=HEADERS
    )

    print_result(
        "DELETE device",
        response.status_code == 200,
        response.status_code
    )


def test_confirm_deletion():
    response = requests.get(
        f"{BASE_URL}/devices/PYTHON-TEST-R1",
        headers=HEADERS
    )

    print_result(
        "Confirm deleted device returns 404",
        response.status_code == 404,
        response.status_code
    )


if __name__ == "__main__":
    print("\nDevNet REST API Automated Tests")
    print("-------------------------------")

    test_authenticated_get()
    test_unauthorised_get()
    test_device_not_found()
    test_create_device()
    test_duplicate_device()
    test_invalid_ip()
    test_update_device()
    test_delete_device()
    test_confirm_deletion()