const form =
    document.getElementById("predictionForm");


const loading =
    document.getElementById("loading");


const result =
    document.getElementById("result");


const resultText =
    document.getElementById("resultText");


const probability =
    document.getElementById("probability");


const progress =
    document.getElementById("progress");


const resultIcon =
    document.getElementById("resultIcon");


const resultMessage =
    document.getElementById("resultMessage");



/* =========================================
   FORM SUBMISSION
========================================= */

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        /* -------------------------------------
           Show loading
        ------------------------------------- */

        loading.classList.remove(
            "hidden"
        );

        result.classList.add(
            "hidden"
        );


        /* -------------------------------------
           Collect patient data
        ------------------------------------- */

        const patientData = {


            age:

                Number(
                    document
                        .getElementById("age")
                        .value
                ),


            sex:

                Number(
                    document
                        .getElementById("sex")
                        .value
                ),


            cp:

                Number(
                    document
                        .getElementById("cp")
                        .value
                ),


            trestbps:

                Number(
                    document
                        .getElementById("trestbps")
                        .value
                ),


            chol:

                Number(
                    document
                        .getElementById("cholesterol")
                        .value
                ),


            fbs:

                Number(
                    document
                        .getElementById("fbs")
                        .value
                ),


            restecg:

                Number(
                    document
                        .getElementById("restecg")
                        .value
                ),


            thalach:

                Number(
                    document
                        .getElementById("thalach")
                        .value
                ),


            exang:

                Number(
                    document
                        .getElementById("exang")
                        .value
                ),


            oldpeak:

                Number(
                    document
                        .getElementById("oldpeak")
                        .value
                ),


            slope:

                Number(
                    document
                        .getElementById("slope")
                        .value
                ),


            ca:

                Number(
                    document
                        .getElementById("ca")
                        .value
                ),


            thal:

                Number(
                    document
                        .getElementById("thal")
                        .value
                )

        };



        /* =====================================
           SEND DATA TO FLASK
        ===================================== */

        try {


            const response =

                await fetch(
                    "http://127.0.0.1:5000/predict",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                patientData
                            )

                    }
                );



            const data =
                await response.json();



            /* ---------------------------------
               Hide loading
            --------------------------------- */

            loading.classList.add(
                "hidden"
            );



            /* ---------------------------------
               Handle backend error
            --------------------------------- */

            if (data.error) {

                alert(
                    "Prediction error: " +
                    data.error
                );

                return;

            }



            /* ---------------------------------
               Show result
            --------------------------------- */

            result.classList.remove(
                "hidden"
            );



            /* ---------------------------------
               Probability
            --------------------------------- */

            const probabilityValue =
                Number(
                    data.probability
                );


            probability.textContent =
                probabilityValue.toFixed(2) +
                "%";



            /* ---------------------------------
               Animate progress bar
            --------------------------------- */

            progress.style.width =
                "0%";


            setTimeout(
                function () {

                    progress.style.width =
                        probabilityValue +
                        "%";

                },
                100
            );



            /* ---------------------------------
               Prediction text
            --------------------------------- */

            resultText.textContent =
                data.result;



            /* ---------------------------------
               Explanation message
            --------------------------------- */

            resultMessage.textContent =
                data.message;



            /* =================================
               HEART DISEASE DETECTED
            ================================= */

            if (data.prediction === 1) {


                resultText.style.color =
                    "#e63964";


                resultIcon.className =
                    "fa-solid fa-triangle-exclamation";


                resultIcon.parentElement.style.background =
                    "#fff0f2";


                resultIcon.parentElement.style.color =
                    "#e63964";


                progress.style.background =
                    "linear-gradient(90deg, #e63964, #ff6b6b)";



            }


            /* =================================
               NO HEART DISEASE
            ================================= */

            else {


                resultText.style.color =
                    "#16a085";


                resultIcon.className =
                    "fa-solid fa-circle-check";


                resultIcon.parentElement.style.background =
                    "#e8f8f3";


                resultIcon.parentElement.style.color =
                    "#16a085";


                progress.style.background =
                    "linear-gradient(90deg, #16a085, #2ecc71)";

            }



            /* ---------------------------------
               Scroll to result
            --------------------------------- */

            result.scrollIntoView({

                behavior: "smooth",

                block: "center"

            });


        }


        /* =====================================
           CONNECTION ERROR
        ===================================== */

        catch (error) {


            loading.classList.add(
                "hidden"
            );


            alert(

                "Unable to connect to the " +
                "prediction server.\n\n" +

                "Please make sure Flask is running."

            );


            console.error(error);

        }

    }
);