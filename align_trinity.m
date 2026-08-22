function out = align_trinity(capsule)
    theta = pi/4; phi = pi/3; f = 35;
    d_cam = capsule.dipole.dir(theta, phi);
    a_cam = capsule.dipole.antipode(theta, phi);
    x_s = f * tan(theta) * cos(phi);
    y_s = f * tan(theta) * sin(phi);
    out.dipole_cam = d_cam;
    out.antipode_cam = a_cam;
    out.sensor_point = [x_s, y_s];
    out.database_server = capsule.database.server;
    out.database_port   = capsule.database.port;
end
