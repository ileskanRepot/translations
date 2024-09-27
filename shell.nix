{ pkgs ? import <nixpkgs> {}}:
  pkgs.mkShell {
    nativeBuildInputs = let
      env = pyPkgs : with pyPkgs; [
        fastapi
        uvicorn
        jinja2
        psycopg2
        python-multipart
      ];
    in with pkgs; [
      (python311.withPackages env)
  ];
}
