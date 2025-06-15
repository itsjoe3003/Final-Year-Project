import React from 'react';

interface OptionsWidgetProps {
  options: string[];
  handleOptionClick: (option: string) => void;
}

const OptionsWidget: React.FC<OptionsWidgetProps> = ({ options, handleOptionClick }) => {
  return (
    <div>
      {options.map((option, index) => (
        <button key={index} onClick={() => handleOptionClick(option)}>
          {option}
        </button>
      ))}
    </div>
  );
};

export default OptionsWidget;
