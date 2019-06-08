$(document).ready(function () {

    $("#switch1").find("input[type=checkbox]").on("change", function () {
        var status = $(this).prop('checked');
        console.log(status, 'switch one');
        if (status) {
            console.log("status is true/Switch on/DEV1");
            data_dev =  { dev : "dev1" };
            $.ajax({
                url: "http://192.168.1.47:5000/switchboard2/",
                type: "POST",
                dataType: "json",
                contentType: 'application/json',
                data: JSON.stringify(data_dev),
                success: function (data) {
                    console.log(data);
                    alert(data);
                },
            });
        } else {
            console.log("status is false/Switch off/DEV1");
            data =  {dev:"dev1"};
            $.ajax({
                url: "http://192.168.1.47:5000/switchboard1/",
                type: "POST",
                dataType:"json",
                contentType: 'application/json',
                data: JSON.stringify(data_dev),
                success: function (data) {
                    console.log(data);
                    alert(data);
                },
            });
        }

        // $.ajax({
        //     url: url,
        //     type: "post",
        //     data: {
        //         status: status
        //     }
        // })
    });

    $("#switch2").find("input[type=checkbox]").on("change", function () {
        var status = $(this).prop('checked');
        console.log(status, 'switch one');
        if (status) {
            console.log("status is true/Switch on/DEV2");
            data_dev =  { dev : "dev2" };
            $.ajax({
                url: "http://192.168.1.47:5000/switchboard2/",
                type: "POST",
                dataType: "json",
                contentType: 'application/json',
                data: JSON.stringify(data_dev),
                success: function (data) {
                    console.log(data);
                    alert(data);
                },
            });
        } else {
            console.log("status is false/Switch off/DEV2");
            data =  {dev:"dev2"};
            $.ajax({
                url: "http://192.168.1.47:5000/switchboard1/",
                type: "POST",
                dataType:"json",
                contentType: 'application/json',
                data: JSON.stringify(data_dev),
                success: function (data) {
                    console.log(data);
                    alert(data);
                },
            });
        }
    });




    $("#switch3").find("input[type=checkbox]").on("change", function () {
        var status = $(this).prop('checked');
        console.log(status, 'switch one');
        if (status) {
            console.log("status is true/Switch on/DEV3");
            data_dev =  { dev : "dev3" };
            $.ajax({
                url: "http://192.168.1.47:5000/switchboard2/",
                type: "POST",
                dataType: "json",
                contentType: 'application/json',
                data: JSON.stringify(data_dev),
                success: function (data) {
                    console.log(data);
                    alert(data);
                },
            });
        } else {
            console.log("status is false/Switch off/DEV3");
            data =  {dev:"dev3"};
            $.ajax({
                url: "http://192.168.1.47:5000/switchboard1/",
                type: "POST",
                dataType:"json",
                contentType: 'application/json',
                data: JSON.stringify(data_dev),
                success: function (data) {
                    console.log(data);
                    alert(data);
                },
            });
        }
    });


    $("#switch4").find("input[type=checkbox]").on("change", function () {
        var status = $(this).prop('checked');
        console.log(status, 'switch one');
        if (status) {
            console.log("Automation ON");
            check =  { auto: "on" };
            $.ajax({
                url: "http://192.168.1.47:5000/automation1/",
                type: "POST",
                dataType: "json",
                contentType: 'application/json',
                data: JSON.stringify(check),
                success: function (data) {
                    console.log(data);
                    alert(data["Automation"]);
                },
            });
        } else {
            console.log("Automation OFF");
            check =  {auto:"off"};
            $.ajax({
                url: "http://192.168.1.47:5000/automation1/",
                type: "POST",
                dataType:"json",
                contentType: 'application/json',
                data: JSON.stringify(check),
                success: function (data) {
                    console.log(data);
                    alert(data["Automation"]);
                },
            });
        }
    });

});