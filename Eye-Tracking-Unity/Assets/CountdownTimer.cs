using UnityEngine;
using UnityEngine.UI;

public class CountdownTimer : MonoBehaviour
{
    [SerializeField] float countdownTime = 10f;
    [SerializeField] Text countdownText;
    [SerializeField] bool isCountdownActive = false;

    private void Start()
    {
        countdownText = GetComponent<Text>();
    }

    private void Update()
    {
        if (isCountdownActive)
        {
            countdownTime -= Time.deltaTime;

            if (countdownTime <= 0f)
            {
                countdownTime = 0f;
                isCountdownActive = false;
                Debug.Log("Countdown finished.");
            }

            countdownText.text = Mathf.Ceil(countdownTime).ToString();
        }
    }

    public void StartCountdown()
    {
        // Start the countdown
        isCountdownActive = true;
    }
}
