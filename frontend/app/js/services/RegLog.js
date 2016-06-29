module.exports = function ($http) {
    return {
        // register new user
        register: function (username, email, password) {
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/register/',
                data: {
                    username: username,
                    email: email,
                    password: password
                }
            });
        },
        
        login: function (username, password) {
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/login/',
                data: {
                    username: username,
                    password: password
                }
            });
        }

    };
};