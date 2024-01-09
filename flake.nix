{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix {
          inherit pkgs;
        })
          mkPoetryApplication
          defaultPoetryOverrides;
      in
      {
        packages = {
          bitlypy = mkPoetryApplication {
            projectDir = self;
            python = pkgs.python311;
            overrides = defaultPoetryOverrides.extend (self: super: {
              flask-sqlalchemy = super.flask-sqlalchemy.overridePythonAttrs
                (
                  old: {
                    buildInputs = (old.buildInputs or [ ]) ++ [ pkgs.python311Packages.flit-core ];
                  }
                );
            });
          };
          default = self.packages.${system}.bitlypy;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.bitlypy ];
          packages = [ pkgs.poetry pkgs.python311 pkgs.litecli ];
        };
      });
}
