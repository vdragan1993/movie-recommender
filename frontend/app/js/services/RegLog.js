module.exports = function ($http) {
    return {
        test: function () {
            return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/test'
            });
        }
    };
};