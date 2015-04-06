window.Lickr = Ember.Application.create();

Lickr.ApplicationSerializer = DS.RESTSerializer.extend({
  primaryKey: '_id',
});

Lickr.ApplicationAdapter = DS.RESTAdapter.extend({
    host: 'http://localhost:8000',
    namespace: 'api'
});