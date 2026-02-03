using UnityEngine;

// Improved drone controller: smooth movement, speed multiplier affected by BOOST/BRAKE gestures.
public class DroneController : MonoBehaviour
{
    public float baseSpeed = 3f;
    public float baseVerticalSpeed = 2f;
    public GestureUDPListener listener; // optional: if using UDP mode

    // smoothing
    private Vector3 velocity = Vector3.zero;
    private float currentSpeedMultiplier = 1.0f;
    private float targetSpeedMultiplier = 1.0f;

    // tuning
    public float accel = 5f; // smooth interpolation speed
    public float multiplierLerpSpeed = 2f;

    void Update()
    {
        string cmd = "";

        if (listener != null && listener.HasCommand())
        {
            cmd = listener.GetCommand();
        }

        // BOOST/BRAKE adjust multiplier immediately
        if (!string.IsNullOrEmpty(cmd))
        {
            cmd = cmd.ToUpper();
            if (cmd == "BOOST")
            {
                targetSpeedMultiplier = 2.2f; // speed up
            }
            else if (cmd == "BRAKE")
            {
                targetSpeedMultiplier = 0.5f; // slow down
            }
        }

        // lerp multiplier for smooth feel
        currentSpeedMultiplier = Mathf.Lerp(currentSpeedMultiplier, targetSpeedMultiplier, Time.deltaTime * multiplierLerpSpeed);

        // Movement: prefer UDP commands (FORWARD/LEFT/RIGHT etc.) else keyboard fallback
        if (!string.IsNullOrEmpty(cmd) && cmd != "BOOST" && cmd != "BRAKE")
        {
            ApplyCommand(cmd);
        }
        else
        {
            // keyboard fallback
            float h = 0f;
            float v = 0f;
            if (Input.GetKey("w")) v = 1f;
            if (Input.GetKey("s")) v = -1f;
            if (Input.GetKey("a")) h = -1f;
            if (Input.GetKey("d")) h = 1f;

            Vector3 desired = new Vector3(h, 0, v);
            desired = desired.normalized * baseSpeed * currentSpeedMultiplier;

            // vertical
            if (Input.GetKey("space"))
                desired += Vector3.up * baseVerticalSpeed * currentSpeedMultiplier;
            if (Input.GetKey(KeyCode.LeftControl))
                desired += Vector3.down * baseVerticalSpeed * currentSpeedMultiplier;

            // smooth move
            transform.Translate(desired * Time.deltaTime, Space.Self);
        }

        // slowly return multiplier to 1 if no BOOST/BRAKE command persists
        targetSpeedMultiplier = Mathf.Lerp(targetSpeedMultiplier, 1.0f, Time.deltaTime * 0.5f);
    }

    void ApplyCommand(string cmd)
    {
        if (string.IsNullOrEmpty(cmd)) return;
        cmd = cmd.ToUpper();

        float h = 0f;
        float v = 0f;
        Vector3 move = Vector3.zero;

        switch (cmd)
        {
            case "FORWARD":
                v = 1f;
                break;
            case "BACK":
                v = -1f;
                break;
            case "LEFT":
                h = -1f;
                break;
            case "RIGHT":
                h = 1f;
                break;
            case "UP":
                transform.Translate(Vector3.up * baseVerticalSpeed * currentSpeedMultiplier * Time.deltaTime, Space.World);
                return;
            case "DOWN":
                transform.Translate(Vector3.down * baseVerticalSpeed * currentSpeedMultiplier * Time.deltaTime, Space.World);
                return;
            case "STOP":
                return;
            default:
                return;
        }

        move = new Vector3(h, 0, v).normalized * baseSpeed * currentSpeedMultiplier;
        transform.Translate(move * Time.deltaTime, Space.Self);
    }
}
