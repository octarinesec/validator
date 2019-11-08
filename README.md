<img src="./images/logo_print.png" width="250")
# Validator

Docker image which invokes security script using Octactl


## Configuration:
| Name                       | Description                                           | Required | Default |
| -------------------------- | ----------------------------------------------------- | -------- | ------- |
| OCTARINE_ACCOUNT           | Octarine account name                                 | Yes      | None    |
| OCTARINE_SESSION_ID        | Octarine session ID                                   | Yes      | None    |
| OCTARINE_SESSION_ACCESSJWT | Octarine session access JWT                           | Yes      | None    |
| OBJECT_DIR                 | Directory or file path with the Kubernetes yaml files | Yes      | None    |
| OCTAINE_POLICY             | Octarine Policy name to use for the validate          | No       | Default |
| OUTPUT_FILE_PATH           | Path to the output file                               | No       | None    |


## How to generate Octarine session id 

Login to Octarine with octactl, user must have admin privileges and run the command `octactl access-key create`.
This will create a new long term session key and will return :
```yaml
token_id: <TOKEN_ID>
api_host: main.octarinesec.com
api_port: 443
session:
  accessjwt: <OCTARINE_SESSION_ACCESSJWT>
  id: <OCTARINE_SESSION_ID>
```

