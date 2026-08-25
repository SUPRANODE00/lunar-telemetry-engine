import json

def load_endo_sun_vector():
    try:
        with open('capsule_solar_vector.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"status": "uninitialized", "error": str(e)}

if __name__ == "__main__":
    print(json.dumps(load_endo_sun_vector(), indent=2))
