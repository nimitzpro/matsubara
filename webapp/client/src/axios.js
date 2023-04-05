export default function ({ $axios }) {

    // Axios interceptor to handle responses that need to be polled
    $axios.onResponse(async response => {

        // Use the 202 response code as an indicator that polling is needed
        if (response.status === 202) {

            console.log("HTTP 202 received, polling operation...");
            console.log("Operation running at " + response.headers.location);

            // Retrieve the initial operation status
            let pollingResponse = await $axios.get(response.headers.location);

            console.log("Operation status is " + pollingResponse.data.status);

            // Loop while the operation is still in progress...
            while(pollingResponse.data.status !== "Succeeded" && pollingResponse.data.status !== "Failed") {

                setTimeout(async function () {
                  pollingResponse = await $axios.get(response.headers.location);

                  console.log("Operation status is " + pollingResponse.data.status);
                }, 2000);
            }

            if (pollingResponse.data.status === "Failed") {
                // Treat failures as exceptions, so they can be handled as such
                throw 'Operation failed!';      
            }
            else {

                console.log("Operation succeeded!");
                console.log("Retrieving resource at " + pollingResponse.data.resourceLocation);

                // Once operation succeeded, return response from final resource location
                return await $axios.get(pollingResponse.data.resourceLocation);
            }
        }

        // If not a 202 response, then return as normal
        return response;
    })
}