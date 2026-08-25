const theta = Math.PI/4;
const phi   = Math.PI/3;

const dipole = [
  Math.sin(theta) * Math.cos(phi),
  Math.sin(theta) * Math.sin(phi),
  Math.cos(theta)
];

const antipode = dipole.map(v => -v);

module.exports = {
  GNSS_ENU_origin: [0,0,0],
  camera_pupil: [0,0,0],
  dipole: dipole,
  antipode: antipode,
  radius_shell: { inner: 1.0, outer: 5.0 },
  database: {
    server: process.env.DB_IP || "192.168.1.15",
    port: process.env.DB_PORT || 5432
  }
};
