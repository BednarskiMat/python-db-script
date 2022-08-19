def format_php(name, folder_name, cli_id, div_id):
    php_string = """<?php

namespace ncs\\batch\client_data_import\customer_profiles;

use ncs\\batch\client_data_import;
use ncs\\batch\client_data_import\sql;

require_once __DIR__ . '/../base_profile.php';
require_once __DIR__ . '/../sql_inserter.php';
require_once __DIR__ . '/../file_import_excel.php';

class ncs_practice extends base_profile{{
	
	public $name = '{name}';
	public $folderName = '{folder_name}'; # case sensitive
	public $cli_id = {cli_id};
	public $div_id = {div_id}; # master division
	public $fileTableNames = ['raci_chart']; # Caution: Do not use table names with special MariaDB characters
	public $recipients = [];
	public $deleteImageFiles = false;
	//public $api_route = '';

	public function identifyFileType(string $filename) : ?string {{
		if(preg_match('/raci_chart.*\.xlsx$/i', $filename)){{
			return 'raci_chart';
		}}
		return null;
	}}

	public function ingestFile(string $filePath, array $import_file_row, object $db) : ?array{{

		$type = $import_file_row['file_type'];

		$import_id = $import_file_row['import_id'];

		$skippedRows = 0;

		if(!in_array($type, $this->fileTableNames)){{
			throw new \Exception("Error: Invalid type '{{$type}}' specified.\\n");
		}}

		if(parent::checkIngestTableForID($type, $import_id, $db)){{
			echo "Error: import_id {{$import_id}} has already been ingested to table {{$type}}.\\n";
			return null;
		}}

		$successCount = 0;
		$errorCount = 0;

		if('raci_chart' === $type){{
			$table = 'raci_chart';

            //[ Excel Column Number => SQL Column Name ]
			$xlsColumnMapping = [
				0 => 'system_tasks',
                1 => 'coverage_level',
                2 => 'priority',
                3 => 'num_rs',
                4 => 'cheselka',
                5 => 'frank',
                6 => 'draeger',
                7 => 'kirsch',
                8 => 'bidwell',
                9 => 'spangler',
                10 => 'taylor',
                11 => 'matt',
                12 => 'stephen',
                13 => 'ranallo',
                14 => 'penttila',
                15 => 'szemplak',
                16 => 'carney',
                17 => 'marketing',
                18 => 'sales',
                19 => 'leadership',
                20 => 'hr',
                21 => 'accouont',
                22 => 'ucc_ops',
                23 => 'liens_ops',
                24 => 'col_ops',
                25 => 'ectobox',
                26 => 'fourim_consulting',
                27 => 'bds',
                28 => 'chad_king',
                29 => 'tec',
                30 => 'kiwi'
			];
			$expectedColumnCount = sizeof($xlsColumnMapping);
		}}


		$xls = new client_data_import\\file_import_excel($filePath);

		# Validate header row 
		if(null === ($headerRow = $xls->getNextRow())){{
			echo "Error: This spreadsheet cannot be parsed. Invalid file format.\\n";
			return null;
		}}

		if(sizeof($headerRow) > $expectedColumnCount){{ # the header row has too many columns
			echo "Notice: The header row contains too many columns. Attempting to trim blank values to expected size.\\n";
			$headerRow = parent::trimArrayToSize($headerRow, $expectedColumnCount);
		}}

		if(sizeof($headerRow) !== $expectedColumnCount){{
			echo "Error: file_import_id '{{$import_id}}' has a header row with " . sizeof($headerRow) . " columns. ";
			echo "Expected: {{$expectedColumnCount}} columns.\\n";

			return null;
		}}

		$stmt = false;
		
		# Process remaining rows
		while(null !== ($row = $xls->getNextRow())){{
			
			# Validate column count
			if(sizeof($row) > $expectedColumnCount){{ # the current row has too many columns, attempt to trim
				$row = parent::trimArrayToSize($row, $expectedColumnCount);
			}}

			if(sizeof($row) !== $expectedColumnCount){{
				echo "Error: Input XLS line # " .$xls->rowNumber . " has " . sizeof($row) . " columns. Expected: {{$expectedColumnCount}}\\n";
				++$errorCount;
				continue;
			}}

			# Row must contain at least one column with non-empty value
			$emptyRow = true;
			foreach($row as $column){{
				if(strlen(trim($column))){{
					$emptyRow = false;
					break;	
				}}
			}}
			if($emptyRow){{
				++$skippedRows;
				continue;
			}}
			
			
			# Assign some SQL columns => values
			$sqlMap = [
				'import_id' => $import_id,
				'line_number' => $xls->rowNumber
			];

			# Auto-assign the rest of SQL columns from $xlsColumnMapping
			foreach($xlsColumnMapping as $colNum => $name){{
				$sqlMap[$name] = trim($row[$colNum]);
			}}
			
			# Attempt SQL insert
			if(false === $stmt){{
				# prepare SQL insert
				$stmt = sql\inserter::prepareInsert($table, $sqlMap, $db);
			}}

			$inserted = $stmt->execute(array_values($sqlMap));

			# Count success or failure
			if($inserted){{
				++$successCount;
			}}
			else{{
				$pdoError = $stmt->errorInfo();
				echo "Warning: SQL Insert failed for XLS Row # " . $xls->rowNumber . ". DB error message: {{$pdoError[2]}}\\n";
				++$errorCount;
			}}

			if($successCount % 500 === 0){{
				echo "Progress: inserted {{$successCount}} rows.\\n";
			}}
            

		}}

		if($skippedRows){{
			echo "Notice: Skipped {{$skippedRows}} empty rows.\\n";
		}}
		return [$successCount, $errorCount];
        


	}}

}}
    """.format(
        name=name,
        folder_name= folder_name, 
        cli_id=cli_id, 
        div_id=div_id,

    )

    return php_string